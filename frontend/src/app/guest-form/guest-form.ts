import { CurrencyPipe, JsonPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import {
  AbstractControl,
  FormBuilder,
  ReactiveFormsModule,
  ValidationErrors,
  Validators,
} from '@angular/forms';
import {
  catchError,
  debounceTime,
  distinctUntilChanged,
  map,
  of,
  scan,
  startWith,
  switchMap,
} from 'rxjs';

import { DiscountService } from '../discounts/discount-service';
import { TicketService } from '../tickets/ticket-service';

/** Local calendar date as YYYY-MM-DD, matching the value format of <input type="date">. */
function todayIso(): string {
  return new Date().toLocaleDateString('en-CA');
}

function notInPast(control: AbstractControl): ValidationErrors | null {
  if (!control.value) return null;
  return control.value < todayIso() ? { past: true } : null;
}

function dateRange(group: AbstractControl): ValidationErrors | null {
  const from = group.get('dateFrom')?.value;
  const to = group.get('dateTo')?.value;
  return from && to && to < from ? { dateRange: true } : null;
}

type QuoteEvent =
  | { kind: 'idle' }
  | { kind: 'loading' }
  | { kind: 'error' }
  | { kind: 'ready'; price: number };

/** The last known price is kept while a new one loads, so the panel never blanks out. */
interface QuoteState {
  price: number | null;
  loading: boolean;
  error: boolean;
}

const IDLE_QUOTE: QuoteState = { price: null, loading: false, error: false };

@Component({
  selector: 'app-guest-form',
  imports: [ReactiveFormsModule, CurrencyPipe, JsonPipe],
  templateUrl: './guest-form.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class GuestForm {
  private readonly fb = inject(FormBuilder);
  private readonly tickets = inject(TicketService);
  private readonly discounts = inject(DiscountService);

  protected readonly today = todayIso();
  protected readonly submitted = signal<unknown>(null);

  protected readonly discountOptions = toSignal(
    this.discounts.getDiscounts().pipe(catchError(() => of([]))),
    { initialValue: [] },
  );

  protected readonly form = this.fb.group(
    {
      firstName: ['', [Validators.required, Validators.maxLength(255)]],
      lastName: ['', [Validators.required, Validators.maxLength(255)]],
      heightCm: [
        null as number | null,
        [Validators.required, Validators.min(30), Validators.max(250)],
      ],
      dateFrom: [todayIso(), [Validators.required, notInPast]],
      dateTo: [''],
      discountId: [''],
    },
    { validators: dateRange },
  );

  /** Re-quotes on load and whenever a date or the discount changes. */
  protected readonly quote = toSignal(
    this.form.valueChanges.pipe(
      debounceTime(250),
      startWith(null),
      map(
        () =>
          [
            this.form.controls.dateFrom.value,
            this.form.controls.dateTo.value,
            this.form.controls.discountId.value,
          ] as [string | null, string | null, string | null],
      ),
      distinctUntilChanged((a, b) => a[0] === b[0] && a[1] === b[1] && a[2] === b[2]),
      switchMap(([from, to, discountId]) => {
        if (!from || this.form.controls.dateFrom.invalid || this.form.hasError('dateRange')) {
          return of<QuoteEvent>({ kind: 'idle' });
        }

        return this.tickets.getPrice(from, to, discountId).pipe(
          map((res) => ({ kind: 'ready', price: res.price }) as QuoteEvent),
          catchError(() => of<QuoteEvent>({ kind: 'error' })),
          startWith<QuoteEvent>({ kind: 'loading' }),
        );
      }),
      scan((state: QuoteState, event: QuoteEvent): QuoteState => {
        switch (event.kind) {
          case 'loading':
            return { ...state, loading: true, error: false };
          case 'ready':
            return { price: event.price, loading: false, error: false };
          case 'error':
            return { ...state, loading: false, error: true };
          case 'idle':
            return IDLE_QUOTE;
        }
      }, IDLE_QUOTE),
    ),
    { initialValue: IDLE_QUOTE },
  );

  /** Mirrors the backend's day count: an empty or equal date_to still bills one day. */
  protected readonly days = computed(() => {
    if (this.quote().price === null) return 0;

    const from = this.form.controls.dateFrom.value;
    const to = this.form.controls.dateTo.value || from;
    if (!from || !to) return 0;

    const diff = (Date.parse(to) - Date.parse(from)) / 86_400_000;
    return diff || 1;
  });

  /** The discount reflected in the current quote, if any. */
  protected readonly appliedDiscount = computed(() => {
    if (this.quote().price === null) return null;

    const id = this.form.controls.discountId.value;
    return this.discountOptions().find((d) => String(d.id) === id) ?? null;
  });

  protected showError(name: string): boolean {
    const control = this.form.get(name)!;
    return control.invalid && (control.touched || control.dirty);
  }

  protected onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitted.set(this.form.getRawValue());
  }
}

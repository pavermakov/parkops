import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';

export interface Discount {
  id: number;
  title: string;
  discount_percent: number;
}

interface DiscountsResponse {
  discounts: Discount[];
}

@Injectable({ providedIn: 'root' })
export class DiscountService {
  private readonly http = inject(HttpClient);

  getDiscounts(): Observable<Discount[]> {
    return this.http
      .get<DiscountsResponse>('/discounts/')
      .pipe(map((res) => res.discounts));
  }
}

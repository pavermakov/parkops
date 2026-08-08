import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface TicketPrice {
  price: number;
}

@Injectable({ providedIn: 'root' })
export class TicketService {
  private readonly http = inject(HttpClient);

  /**
   * `dateTo` is always sent: the API defaults a missing date_to to today, which
   * produces a negative price for a future date_from.
   */
  getPrice(
    dateFrom: string,
    dateTo?: string | null,
    discountId?: string | null,
  ): Observable<TicketPrice> {
    let params = new HttpParams()
      .set('date_from', dateFrom)
      .set('date_to', dateTo || dateFrom);

    if (discountId) {
      params = params.set('discount_id', discountId);
    }

    return this.http.get<TicketPrice>('/tickets/price/', { params });
  }
}

import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ClassificationResult {
  label: string;
  label_probabilities: Record<string, number>;
}

@Injectable({ providedIn: 'root' })
export class ClassifierService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:5000/classification/classify';

  classify(file: File): Observable<ClassificationResult> {
    const form = new FormData();
    form.append('image', file);
    return this.http.post<ClassificationResult>(this.apiUrl, form);
  }
}

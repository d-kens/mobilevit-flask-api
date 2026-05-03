import { Component, ElementRef, inject, signal, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClassifierService, ClassificationResult } from './classifier.service';

type AppState = 'idle' | 'loading' | 'result' | 'error';

const CATEGORY_META: Record<string, { color: string; icon: string; severity: 'disease' | 'healthy' }> = {
  'Early Blight':       { color: '#f97316', icon: '🍂', severity: 'disease' },
  'Late Blight':        { color: '#ef4444', icon: '🦠', severity: 'disease' },
  'Septoria Leaf Spot': { color: '#eab308', icon: '🔴', severity: 'disease' },
  'Healthy':            { color: '#22c55e', icon: '✅', severity: 'healthy' },
};

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  @ViewChild('fileInput') fileInputRef!: ElementRef<HTMLInputElement>;

  private classifier = inject(ClassifierService);

  state = signal<AppState>('idle');
  preview = signal<string | null>(null);
  result = signal<ClassificationResult | null>(null);
  errorMsg = signal<string>('');
  dragOver = signal(false);
  selectedFile = signal<File | null>(null);

  get sortedProbs(): { label: string; value: number; color: string; icon: string }[] {
    const r = this.result();
    if (!r) return [];
    return Object.entries(r.label_probabilities)
      .map(([label, value]) => ({
        label,
        value,
        color: CATEGORY_META[label]?.color ?? '#6b7280',
        icon: CATEGORY_META[label]?.icon ?? '🌿',
      }))
      .sort((a, b) => b.value - a.value);
  }

  get topResultMeta() {
    const r = this.result();
    if (!r) return null;
    const label = this.toDisplayLabel(r.label);
    return CATEGORY_META[label] ?? null;
  }

  toDisplayLabel(raw: string): string {
    return raw.replace(/\b\w/g, c => c.toUpperCase());
  }

  onDragOver(e: DragEvent) {
    e.preventDefault();
    this.dragOver.set(true);
  }

  onDragLeave() {
    this.dragOver.set(false);
  }

  onDrop(e: DragEvent) {
    e.preventDefault();
    this.dragOver.set(false);
    const file = e.dataTransfer?.files?.[0];
    if (file) this.loadFile(file);
  }

  onFileSelected(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) this.loadFile(file);
  }

  openPicker() {
    this.fileInputRef.nativeElement.click();
  }

  loadFile(file: File) {
    if (!file.type.match(/image\/(jpeg|jpg|png)/)) {
      this.errorMsg.set('Only JPG and PNG files are supported.');
      this.state.set('error');
      return;
    }
    this.selectedFile.set(file);
    const reader = new FileReader();
    reader.onload = () => this.preview.set(reader.result as string);
    reader.readAsDataURL(file);
    this.state.set('idle');
    this.result.set(null);
  }

  classify() {
    const file = this.selectedFile();
    if (!file) return;
    this.state.set('loading');
    this.classifier.classify(file).subscribe({
      next: (res) => {
        this.result.set(res);
        this.state.set('result');
      },
      error: () => {
        this.errorMsg.set('Failed to reach the classification API. Make sure the Flask server is running on port 5000.');
        this.state.set('error');
      },
    });
  }

  reset() {
    this.state.set('idle');
    this.preview.set(null);
    this.result.set(null);
    this.selectedFile.set(null);
    this.fileInputRef.nativeElement.value = '';
  }

  pct(value: number): string {
    return (value * 100).toFixed(1) + '%';
  }
}

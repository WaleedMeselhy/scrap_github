import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ScrapyJobsComponent } from './scrapy-jobs.component';

describe('ScrapyJobsComponent', () => {
  let component: ScrapyJobsComponent;
  let fixture: ComponentFixture<ScrapyJobsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ScrapyJobsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ScrapyJobsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

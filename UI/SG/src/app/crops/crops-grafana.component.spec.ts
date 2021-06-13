import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CropsGrafanaComponent } from './crops-grafana.component';

describe('CropsGrafanaComponent', () => {
  let component: CropsGrafanaComponent;
  let fixture: ComponentFixture<CropsGrafanaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CropsGrafanaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CropsGrafanaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

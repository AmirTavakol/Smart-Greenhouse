import { TestBed } from '@angular/core/testing';

import { CropsGrafanaServiceService } from './crops-grafana-service.service';

describe('CropsGrafanaServiceService', () => {
  let service: CropsGrafanaServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CropsGrafanaServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

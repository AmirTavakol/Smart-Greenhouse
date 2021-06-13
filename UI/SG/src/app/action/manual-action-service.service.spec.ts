import { TestBed } from '@angular/core/testing';

import { ManualActionServiceService } from './manual-action-service.service';

describe('ManualActionServiceService', () => {
  let service: ManualActionServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ManualActionServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

import { TestBed } from '@angular/core/testing';

import { EndrDecrServiceService } from './endr-decr-service.service';

describe('EndrDecrServiceService', () => {
  let service: EndrDecrServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EndrDecrServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

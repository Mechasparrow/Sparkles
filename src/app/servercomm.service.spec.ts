import { TestBed, inject } from '@angular/core/testing';

import { ServercommService } from './servercomm.service';

describe('ServercommService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ServercommService]
    });
  });

  it('should be created', inject([ServercommService], (service: ServercommService) => {
    expect(service).toBeTruthy();
  }));
});

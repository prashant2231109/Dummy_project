import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListComponents } from './list';

describe('List', () => {
  let component: ListComponents;
  let fixture: ComponentFixture<ListComponents>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListComponents],
    }).compileComponents();

    fixture = TestBed.createComponent(ListComponents);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

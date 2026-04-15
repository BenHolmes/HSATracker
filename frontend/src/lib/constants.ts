/**
 * Ordered list of HSA-eligible expense categories.
 *
 * Mirrors the HsaCategory enum in backend/app/constants.py. The order here
 * controls how categories appear in dropdowns and filter selects throughout
 * the UI. Update both files together when adding new categories.
 */

import type { HsaCategory } from '../types'

/**
 * All tax years with known IRS HSA contribution limits, newest first.
 *
 * Mirrors the keys of CONTRIBUTION_LIMITS in backend/app/constants.py.
 * Update both files together when the IRS publishes limits for a new year.
 */
export const CONTRIBUTION_TAX_YEARS: readonly number[] = [
  2026, 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017,
  2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007,
  2006, 2005, 2004,
]

export const HSA_CATEGORIES: readonly HsaCategory[] = [
  'doctors_visits',
  'prescription_drugs',
  'dental_care',
  'vision_care',
  'mental_health',
  'physical_therapy',
  'chiropractic',
  'acupuncture',
  'hospital_services',
  'surgery',
  'lab_tests',
  'medical_equipment',
  'hearing_aids',
  'menstrual_products',
  'birth_control',
  'fertility_treatment',
  'smoking_cessation',
  'weight_loss_program',
  'long_term_care',
  'transportation',
  'insurance_premiums',
  'other_eligible',
] as const

/**
 * Ordered list of HSA-eligible expense categories.
 *
 * Mirrors the HsaCategory enum in backend/app/constants.py. The order here
 * controls how categories appear in dropdowns and filter selects throughout
 * the UI. Update both files together when adding new categories.
 */

import type { HsaCategory } from '../types'

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

import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export const registerSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  display_name: z.string().min(2, 'Name must be at least 2 characters').max(100),
});

export const reportSchema = z.object({
  title: z.string().min(5, 'Title must be at least 5 characters').max(300),
  description: z.string().min(20, 'Description must be at least 20 characters'),
  report_type: z.enum([
    'concern',
    'feedback',
    'corruption_tip',
    'progress_update',
    'delay_report',
  ]),
  lgu_id: z.number().positive(),
  project_id: z.number().positive().optional(),
  is_anonymous: z.boolean().default(false),
  latitude: z.number().optional(),
  longitude: z.number().optional(),
  address: z.string().optional(),
});

export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;
export type ReportFormData = z.infer<typeof reportSchema>;

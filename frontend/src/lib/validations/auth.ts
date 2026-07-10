import { z } from "zod";

export const passwordSchema = z
  .string()
  .min(8, "Minimum 8 characters")
  .max(64, "Maximum 64 characters")
  .regex(/[A-Z]/, "Contains uppercase letter")
  .regex(/[a-z]/, "Contains lowercase letter")
  .regex(/[0-9]/, "Contains number")
  .regex(/[!@#$%^&*(),.?":{}|<>]/, "Contains special character")
  .refine((s) => !s.includes(" "), "No spaces allowed");

export const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

export const registerSchema = z
  .object({
    first_name: z.string().min(2, "First name is too short").optional(),
    last_name: z.string().min(2, "Last name is too short").optional(),
    email: z.string().email("Invalid email address"),
    password: passwordSchema,
    confirm_password: z.string(),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords don't match",
    path: ["confirm_password"],
  });

export const forgotPasswordSchema = z.object({
  email: z.string().email("Invalid email address"),
});

export const resetPasswordSchema = z
  .object({
    password: passwordSchema,
    confirm_password: z.string(),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords don't match",
    path: ["confirm_password"],
  });

export type LoginInput = z.infer<typeof loginSchema>;
export type RegisterInput = z.infer<typeof registerSchema>;
export type ForgotPasswordInput = z.infer<typeof forgotPasswordSchema>;
export type ResetPasswordInput = z.infer<typeof resetPasswordSchema>;

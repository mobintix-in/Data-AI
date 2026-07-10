"use client";

import { useState, Suspense } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { resetPasswordSchema, ResetPasswordInput } from "@/lib/validations/auth";
import { api } from "@/services/api";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Eye, EyeOff, Loader2, Check, X } from "lucide-react";

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ResetPasswordInput>({
    resolver: zodResolver(resetPasswordSchema),
  });

  const password = watch("password", "");

  const validationRules = [
    { label: "Minimum 8 characters", test: (p: str) => p.length >= 8 },
    { label: "Maximum 64 characters", test: (p: str) => p.length > 0 && p.length <= 64 },
    { label: "Contains uppercase letter", test: (p: str) => /[A-Z]/.test(p) },
    { label: "Contains lowercase letter", test: (p: str) => /[a-z]/.test(p) },
    { label: "Contains number", test: (p: str) => /[0-9]/.test(p) },
    { label: "Contains special character", test: (p: str) => /[!@#$%^&*(),.?":{}|<>]/.test(p) },
    { label: "No spaces allowed", test: (p: str) => p.length > 0 && !p.includes(" ") },
  ];

  if (!token) {
    return (
      <div className="text-center p-8 text-red-500 bg-white rounded-xl shadow-xl dark:bg-gray-800">
        <p>Invalid or missing reset token.</p>
        <Link href="/login" className="mt-4 inline-block text-blue-600 hover:underline">Go to Login</Link>
      </div>
    );
  }

  const onSubmit = async (data: ResetPasswordInput) => {
    setIsLoading(true);
    setError("");
    try {
      await api.post("/auth/reset-password", { token, new_password: data.password });
      setSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to reset password.");
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div className="w-full max-w-md space-y-8 rounded-xl bg-white p-8 text-center shadow-xl dark:bg-gray-800">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
          <Check className="h-6 w-6 text-green-600" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Password Reset</h2>
        <p className="text-gray-600 dark:text-gray-400">
          Your password has been reset successfully.
        </p>
        <Link href="/login" className="mt-4 block text-blue-600 hover:underline">
          Go to login
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full max-w-md space-y-8 rounded-xl bg-white p-8 shadow-xl dark:bg-gray-800">
      <div className="text-center">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white">Reset Password</h2>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">Enter your new password</p>
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4 text-sm text-red-700 dark:bg-red-900/50 dark:text-red-200">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">New Password</label>
          <div className="relative mt-1">
            <input
              {...register("password")}
              type={showPassword ? "text" : "password"}
              className="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
        </div>

        <div className="space-y-1 text-sm mt-2">
          {validationRules.map((rule, idx) => {
            const isValid = rule.test(password);
            return (
              <div key={idx} className={`flex items-center space-x-2 ${isValid ? 'text-green-600' : 'text-gray-500 dark:text-gray-400'}`}>
                {isValid ? <Check size={16} /> : <X size={16} />}
                <span>{rule.label}</span>
              </div>
            );
          })}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Confirm Password</label>
          <input
            {...register("confirm_password")}
            type="password"
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
          />
          {errors.confirm_password && <p className="mt-1 text-sm text-red-600">{errors.confirm_password.message}</p>}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="flex w-full justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isLoading ? <Loader2 className="animate-spin" size={20} /> : "Reset Password"}
        </button>
      </form>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Suspense fallback={<div className="flex items-center space-x-2"><Loader2 className="animate-spin text-blue-600" /><span>Loading...</span></div>}>
        <ResetPasswordForm />
      </Suspense>
    </div>
  );
}

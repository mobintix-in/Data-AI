"use client";

import { useEffect, useState, Suspense } from "react";
import { api } from "@/services/api";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Loader2, Check, XCircle } from "lucide-react";

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("Invalid or missing verification token.");
      return;
    }

    const verify = async () => {
      try {
        const res = await api.get(`/auth/verify-email?token=${token}`);
        setStatus("success");
        setMessage(res.data.msg);
      } catch (err: any) {
        setStatus("error");
        setMessage(err.response?.data?.detail || "Email verification failed.");
      }
    };

    verify();
  }, [token]);

  return (
    <div className="w-full max-w-md space-y-8 rounded-xl bg-white p-8 text-center shadow-xl dark:bg-gray-800">
      {status === "loading" && (
        <div className="flex flex-col items-center justify-center space-y-4 py-8">
          <Loader2 className="h-12 w-12 animate-spin text-blue-600" />
          <p className="text-gray-600 dark:text-gray-400">Verifying your email...</p>
        </div>
      )}

      {status === "success" && (
        <>
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
            <Check className="h-8 w-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Email Verified!</h2>
          <p className="text-gray-600 dark:text-gray-400">{message}</p>
          <Link href="/login" className="mt-6 inline-block w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
            Continue to Login
          </Link>
        </>
      )}

      {status === "error" && (
        <>
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-red-100">
            <XCircle className="h-8 w-8 text-red-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Verification Failed</h2>
          <p className="text-gray-600 dark:text-gray-400">{message}</p>
          <Link href="/login" className="mt-6 inline-block text-blue-600 hover:underline">
            Go to Login
          </Link>
        </>
      )}
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Suspense fallback={<div className="flex items-center space-x-2"><Loader2 className="animate-spin text-blue-600" /><span>Loading...</span></div>}>
        <VerifyEmailContent />
      </Suspense>
    </div>
  );
}

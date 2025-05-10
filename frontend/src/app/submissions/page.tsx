"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function SubmissionsPage() {
    const router = useRouter();

    useEffect(() => {
        router.push('/user');
    }, [router]);

    return null;
}

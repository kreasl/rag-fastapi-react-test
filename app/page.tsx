'use client';

import React from "react";

import Applications from "@/app/components/Applications";

export default function Home() {
  return <div>
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Applicants</h1>
      <Applications/>
    </main>
  </div>;
}

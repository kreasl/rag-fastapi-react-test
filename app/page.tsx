'use client';

import React from "react";

import CvList from "@/app/components/CvList";

export default function Home() {
  return <div>
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Applicants</h1>
      <CvList/>
    </main>
  </div>;
}

// app/entities/[id]/page.tsx
'use client';

import { useQuery } from '@tanstack/react-query';
import {ChevronLeft, Download} from 'lucide-react';
import React from "react";
import Link from "next/link";

interface EntityDetails {
    id: string;
    name: string;
    description: string;
    path: string;
    details: string;
    uploaded: string;
}

const API_ROOT_URL = 'http://localhost:8000';

export default function EntityDetailsPage({ params }: { params: { id: string } }) {
    const { data, isLoading, isError } = useQuery<EntityDetails>({
        queryKey: ['entity', params.id],
        queryFn: async () => {
            const res = await fetch(`${API_ROOT_URL}/api/cv/${params.id}`);
            if (!res.ok) throw new Error('Failed to fetch entity');
            return res.json();
        },
    });

    if (isLoading) return <div>Loading...</div>;
    if (isError) return <div>Error loading entity</div>;
    if (!data) return null;

    return (
        <div className="container mx-auto p-6">
            <div className="mb-6">
                <Link
                    href="/"
                    className="text-gray-600 hover:text-gray-900 inline-flex items-center"
                >
                    <ChevronLeft className="h-4 w-4 mr-1"/>
                    Back to list
                </Link>
            </div>
            <div className="bg-white rounded-lg shadow-md p-6 mb-4">
                <div className="flex justify-between items-start">
                    <h1 className="text-2xl font-bold">{data.name}</h1>
                    <a
                        href={`http://localhost:8000/${data.path}`}
                        download
                        className="p-2 hover:bg-gray-100 rounded-full"
                        title="Download CV"
                    >
                        <Download className="h-5 w-5 text-gray-600"/>
                    </a>
                </div>

                <p className="text-gray-600 mt-4">{data.description}</p>
                <div className="mt-6">
                    <h2 className="text-lg font-semibold">Details</h2>
                    <p className="mt-2 whitespace-pre-wrap">{data.details}</p>
                </div>
                <div className="mt-6 text-sm text-gray-500">
                    Uploaded: {data.uploaded}
                </div>
            </div>
            <Link
                href={`/cv/${data.id}/edit`}
                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 relative"
            >
                Edit
            </Link>
        </div>
    );
}

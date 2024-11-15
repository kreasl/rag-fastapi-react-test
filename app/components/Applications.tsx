'use client';

import { useQuery } from '@tanstack/react-query';
import Link from "next/link";
import { Download } from 'lucide-react';

interface Application {
    id: string;
    name: string;
    description: string;
    path: string;
}

const API_ROOT_URL = 'http://localhost:8000';
const APPLICATIONS_URL = `${API_ROOT_URL}/api/applications`;

const fetchEntities = async (): Promise<Application[]> => {
    const response = await fetch(APPLICATIONS_URL);
    if (!response.ok) {
        throw new Error('Failed to fetch entities');
    }
    return response.json();
};

export default function Applications() {
    const {data, isLoading, isError, error} = useQuery({
        queryKey: ['applications'],
        queryFn: fetchEntities,
    });

    if (isLoading) {
        return (
            <div className="flex items-center justify-center p-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"/>
            </div>
        );
    }

    if (isError) {
        return (
            <div className="text-red-500 p-4">
                Error: {error instanceof Error ? error.message : 'Something went wrong'}
            </div>
        );
    }

    return (
        <div className="grid gap-4">
            {data?.map((application, index) => (
                <div
                    key={index}
                    className="relative border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                >
                    <Link href={`/application/${application.id}`} className="block">
                        <h3 className="font-semibold text-lg">{application.name}</h3>
                    </Link>
                    {application.path && (
                        <a
                            href={`http://localhost:8000/${application.path}`}
                            download
                            className="absolute top-4 right-4 p-2 hover:bg-gray-100 rounded-full"
                            title="Download CV"
                        >
                            <Download className="h-5 w-5 text-gray-600"/>
                        </a>
                    )}
                </div>
            ))}
            <div>
                <Link
                    href="/application/new"
                    className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                    Add New
                </Link>
            </div>
        </div>
    );
};

'use client';

import { useQuery } from '@tanstack/react-query';
import Link from "next/link";
import { Download } from 'lucide-react';

interface CV {
    id: string;
    name: string;
    description: string;
    path: string;
}

interface FetchInterface {
    cvs: CV[];
}

const API_ROOT_URL = 'http://localhost:8000';
const CV_LIST_URL = `${API_ROOT_URL}/api/cv`;

const fetchEntities = async (): Promise<FetchInterface> => {
    const response = await fetch(CV_LIST_URL);
    if (!response.ok) {
        throw new Error('Failed to fetch entities');
    }
    return response.json();
};

const EntityList = () => {
    const {data, isLoading, isError, error} = useQuery({
        queryKey: ['cvs'],
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
            {data?.cvs.map((cv, index) => (
                <div
                    key={index}
                    className="relative border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                >
                    <Link href={`/cv/${cv.id}`} className="block">
                        <h3 className="font-semibold text-lg">{cv.name}</h3>
                    </Link>
                    {cv.path && (
                        <a
                            href={`http://localhost:8000/${cv.path}`}
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
                    href="/cv/new"
                    className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                    Add New
                </Link>
            </div>
        </div>
    );
};

export default EntityList;

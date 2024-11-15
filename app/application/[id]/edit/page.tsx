'use client';

import ApplicationForm from '@/app/components/ApplicationForm';
import { useQuery } from '@tanstack/react-query';

const API_ROOT_URL = 'http://localhost:8000';

export default function EditEntityPage({ params }: { params: { id: string } }) {
    const { data, isLoading, isError } = useQuery({
        queryKey: ['entity', params.id],
        queryFn: async () => {
            const res = await fetch(`${API_ROOT_URL}/api/application/${params.id}`);
            if (!res.ok) throw new Error('Failed to fetch entity');
            return res.json();
        },
    });

    if (isLoading) {
        return (
            <div className="max-w-2xl mx-auto p-6">
                <div className="animate-pulse">
                    <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
                    <div className="h-[400px] bg-gray-200 rounded"></div>
                </div>
            </div>
        );
    }

    if (isError) {
        return (
            <div className="max-w-2xl mx-auto p-6">
                <div className="bg-red-50 text-red-500 p-4 rounded-md">
                    Failed to load data
                </div>
            </div>
        );
    }

    return <ApplicationForm initialData={data} />;
}
// app/components/EntityForm.tsx
'use client';

import { FormEvent } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import {ChevronLeft, Download} from 'lucide-react';
import Link from 'next/link';

interface EntityFormProps {
    initialData?: {
        id?: string;
        name: string;
        description: string;
        path?: string;
    };
}

const API_ROOT_URL = 'http://localhost:8000';

export default function CvForm({ initialData }: EntityFormProps) {
    const router = useRouter();
    const isEditing = !!initialData?.id;

    const mutation = useMutation({
        mutationFn: async (formData: FormData) => {
            const url = isEditing
                ? `/api/entities/${initialData.id}`
                : '/api/entities';

            const response = await fetch(url, {
                method: isEditing ? 'PUT' : 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Failed to save');
            return response.json();
        },
        onSuccess: () => {
            router.push('/entities');
        },
    });

    const onSubmit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        mutation.mutate(formData);
    };

    return (
        <div className="max-w-2xl mx-auto p-6">
            <div className="mb-6">
                <Link
                    href="/"
                    className="text-gray-600 hover:text-gray-900 inline-flex items-center"
                >
                    <ChevronLeft className="h-4 w-4 mr-1" />
                    Back to list
                </Link>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
                <h1 className="text-2xl font-bold mb-6">
                    {isEditing ? 'Edit Applicant' : 'Create New Applicant'}
                </h1>

                <form onSubmit={onSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                            Name
                        </label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            defaultValue={initialData?.name}
                            required
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    <div>
                        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                            Description
                        </label>
                        <textarea
                            id="description"
                            name="description"
                            defaultValue={initialData?.description}
                            required
                            rows={4}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    {initialData?.path ? (
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-sm text-gray-600">Current file:</span>
                            <a
                                href={`${API_ROOT_URL}/${initialData.path}`}
                                download
                                title="Download current file"
                                className="inline-flex items-center text-blue-500 hover:text-blue-600"
                            >
                                <Download className="h-4 w-4 mr-1" />
                                Download
                            </a>
                        </div>
                    ) : null}

                    <div>
                        <label htmlFor="file" className="block text-sm font-medium text-gray-700 mb-1">
                            File
                        </label>
                        <input
                            type="file"
                            id="file"
                            name="file"
                            required={!isEditing}
                            className="w-full"
                        />
                    </div>

                    <div className="flex justify-end gap-3">
                        <Link
                            href="/"
                            className="px-4 py-2 text-gray-600 hover:text-gray-800"
                        >
                            Cancel
                        </Link>
                        <button
                            type="submit"
                            disabled={mutation.isPending}
                            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                        >
                            {mutation.isPending
                                ? 'Saving...'
                                : isEditing
                                    ? 'Update'
                                    : 'Create'}
                        </button>
                    </div>

                    {mutation.isError && (
                        <div className="text-red-500 text-sm mt-2">
                            {mutation.error ? mutation.error.message : 'Failed to save'}
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
}

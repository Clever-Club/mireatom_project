import { useUserStore } from "@/stores/userStore";

export async function apiFetch(endpoint: string, options: RequestInit = {}, useToken: boolean = true) {
    const baseUrl = import.meta.env.VITE_API_BASE_URL;

    const userStore = useUserStore();
    const token = userStore.token || '';

    const headers = new Headers(options.headers || {});
    if (useToken) {
        headers.set('Authorization', `Bearer ${token}`);
    }

    const response = await fetch(`${baseUrl}/${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return response.json();
}
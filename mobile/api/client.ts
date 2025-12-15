import {
    clearTokens,
    getAccessToken,
    getRefreshToken,
    setAccessToken,
    setRefreshToken,
} from "@/utils/auth-storage";
import axios from "axios";

const apiClient = axios.create({
    baseURL: process.env.EXPO_PUBLIC_API_URL,
    timeout: 1000,
});

apiClient.interceptors.request.use(async (config) => {
    const token = await getAccessToken();
    if (token) {
        config.headers = config.headers ?? {};
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

let isRefreshing = false;
let queue: Array<(token: string | null) => void> = [];

function flushQueue(token: string | null) {
    queue.forEach((cb) => cb(token));
    queue = [];
}

async function refreshAccessToken() {
    const refresh = await getRefreshToken();
    if (!refresh) throw new Error("No refresh token");

    const res = await axios.post(
        `${process.env.EXPO_PUBLIC_API_URL}/token/refresh/`,
        { refresh },
        { timeout: 1000 }
    );

    const newAccess = res.data?.access;
    const newRefresh = res.data?.refresh;

    if (!newAccess) throw new Error("No access token in refresh response");

    await setAccessToken(newAccess);
    if (newRefresh) await setRefreshToken(newRefresh);

    return newAccess as string;
}

apiClient.interceptors.response.use(
    (res) => res,
    async (error) => {
        const original = error.config;
        const status = error?.response?.status;

        const url: string = original?.url ?? "";
        const isAuthEndpoint =
            url.includes("/token/") || url.includes("/token/refresh/");

        if (status === 401 && isAuthEndpoint) {
            throw error;
        }

        if (status !== 401 || original?._retry) {
            throw error;
        }

        const refresh = await getRefreshToken();
        if (!refresh) {
            throw error;
        }

        original._retry = true;

        if (isRefreshing) {
            return new Promise((resolve, reject) => {
                queue.push((token) => {
                    if (!token) return reject(error);
                    original.headers = original.headers ?? {};
                    original.headers.Authorization = `Bearer ${token}`;
                    resolve(apiClient(original));
                });
            });
        }

        isRefreshing = true;

        try {
            const newAccess = await refreshAccessToken();
            flushQueue(newAccess);

            original.headers = original.headers ?? {};
            original.headers.Authorization = `Bearer ${newAccess}`;
            return apiClient(original);
        } catch (e) {
            flushQueue(null);
            await clearTokens();
            throw e;
        } finally {
            isRefreshing = false;
        }
    }
);

export default apiClient;

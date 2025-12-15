import apiClient from '@/api/client';

type RegisterResponse = {
    id: number;
    email: string;
    date_joined: string;
}

type TokensResponse = {
    access: string;
    refresh: string;
}

export const registerUser = async (payload: { email: string, password: string, passwordConfirmation: string }): Promise<RegisterResponse> => {
    const response = await apiClient.post('/register/', {
        email: payload.email,
        password: payload.password,
        password_confirmation: payload.passwordConfirmation,
    });
    return response.data;
}


export const loginUser = async (payload: {
    email: string;
    password: string;
}): Promise<TokensResponse> => {
    const response = await apiClient.post("/token/", payload);
    return response.data;
};

export const refreshToken = async (refresh: string): Promise<TokensResponse> => {
    const response = await apiClient.post("/token/refresh/", { refresh });
    return response.data;
};
import { clearTokens, getAccessToken, saveTokens } from "@/utils/auth-storage";
import { useRouter } from "expo-router";
import React from 'react';

type AuthContextType = {
    isAuthenticated: boolean;
    login: (tokens: { accessToken: string; refreshToken: string }) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = React.createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = React.useState(false);

    React.useEffect(() => {
        (async () => {
            const access = await getAccessToken();
            setIsAuthenticated(!!access);
        })();
    }, []);

    const login = async (tokens: { accessToken: string; refreshToken: string }) => {
        await saveTokens({ access: tokens.accessToken, refresh: tokens.refreshToken });
        setIsAuthenticated(true);
    };

    const logout = async () => {
        await clearTokens();
        setIsAuthenticated(false);
        router.replace('/');
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = (): AuthContextType => {
    const context = React.useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}

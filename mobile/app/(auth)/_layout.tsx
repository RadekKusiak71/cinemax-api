import { Stack } from "expo-router";

const AuthLayout = () => {
    return (
        <Stack>
            <Stack.Screen name="login-view" options={{ headerShown: false }} />
            <Stack.Screen name="register-view" options={{ headerShown: false }} />
        </Stack>
    )
};

export default AuthLayout;
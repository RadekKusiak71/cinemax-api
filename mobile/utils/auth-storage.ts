import * as SecureStore from "expo-secure-store";

async function saveTokens({ access, refresh }: { access: string, refresh: string }) {
    await setAccessToken(access);
    await setRefreshToken(refresh);
}

async function getAccessToken() {
    return SecureStore.getItemAsync("accessToken");
}
async function getRefreshToken() {
    return SecureStore.getItemAsync("refreshToken");
}
async function setAccessToken(token: string) {
    await SecureStore.setItemAsync("accessToken", token, {
        keychainAccessible: SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
    });
}
async function setRefreshToken(token: string) {
    await SecureStore.setItemAsync("refreshToken", token, {
        keychainAccessible: SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
    });
}
async function clearTokens() {
    await SecureStore.deleteItemAsync("accessToken");
    await SecureStore.deleteItemAsync("refreshToken");
}

export { getAccessToken, getRefreshToken, setAccessToken, setRefreshToken, clearTokens, saveTokens };
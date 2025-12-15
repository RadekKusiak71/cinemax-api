import Button from '@/components/button';
import ScreenHeader from '@/components/screen-header';
import { theme } from "@/constants/theme";
import { useAuth } from "@/context/auth-context";
import React from 'react';
import { StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const SettingsScreen = () => {
    const { logout } = useAuth();

    return (
        <SafeAreaView style={styles.container}>
            <ScreenHeader title="Settings" />

            <View style={styles.content}>
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Account</Text>
                    <Button title="Logout" onPress={logout} />
                </View>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: theme.colors.background,
    },
    content: {
        flex: 1,
        padding: 20,
    },
    section: {
        marginBottom: 30,
    },
    sectionTitle: {
        fontSize: 14,
        fontWeight: '600',
        color: theme.colors.textMuted,
        marginBottom: 10,
        textTransform: 'uppercase',
        letterSpacing: 1,
    },
});

export default SettingsScreen;
import { useFocusEffect, useLocalSearchParams, useRouter } from "expo-router";
import * as WebBrowser from "expo-web-browser";
import React, { useCallback, useRef } from "react";
import { Alert, StyleSheet, Text, View } from "react-native";

import { theme } from "@/constants/theme";

WebBrowser.maybeCompleteAuthSession();

type Params = {
    status?: "success" | "cancel" | string;
    reservation_id?: string;
    session_id?: string;
};

export default function PaymentReturnView() {
    const router = useRouter();
    const shownRef = useRef(false);
    const { status, reservation_id } = useLocalSearchParams<Params>();

    useFocusEffect(
        useCallback(() => {
            if (shownRef.current) return;
            shownRef.current = true;

            const reservationId = reservation_id ? Number(reservation_id) : NaN;

            const next = () => {
                if (status === "success") {
                    router.replace("/(dashboard)/movies-list-view");
                    return;
                }

                if (Number.isFinite(reservationId)) {
                    router.replace({
                        pathname: "/reservation/[booking_id]/reservation-details-view",
                        params: { booking_id: String(reservationId) },
                    } as any);
                    return;
                }

                router.replace("/(dashboard)/movies-list-view");
            };

            const title =
                status === "success"
                    ? "Payment successful"
                    : status === "cancel"
                        ? "Payment cancelled"
                        : "Payment return";

            const message =
                status === "success"
                    ? "Your payment was completed."
                    : status === "cancel"
                        ? "You cancelled the payment."
                        : "Returning to the app.";

            Alert.alert(title, message, [{ text: "OK", onPress: next }]);
        }, [reservation_id, router, status])
    );

    return (
        <View style={styles.container}>
            <Text style={styles.text}>Returning to the app...</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: theme.colors.background,
        padding: 16,
    },
    text: {
        color: theme.colors.textMuted,
    },
});

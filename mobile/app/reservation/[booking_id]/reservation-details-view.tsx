import { useCancelReservation, useCreateCheckoutSession, useReservationDetail } from "@/api/reservations";
import Button from "@/components/button";
import ErrorScreen from "@/components/ui/error-screen";
import LoadingScreen from "@/components/ui/loading-screen";
import { theme } from "@/constants/theme";
import { useAuth } from "@/context/auth-context";
import { useFocusEffect } from "@react-navigation/native";
import * as Linking from "expo-linking";
import { useLocalSearchParams, useRouter } from "expo-router";
import * as WebBrowser from "expo-web-browser";
import React, { useCallback, useEffect, useMemo } from "react";
import { Alert, AppState, ScrollView, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const ReservationDetailsView = () => {
    const router = useRouter();
    const { isAuthenticated } = useAuth();

    const { booking_id, showtime_id } = useLocalSearchParams<{ booking_id: string; showtime_id?: string }>();

    const bookingId = Number(booking_id);
    const showtimeIdFromParams = showtime_id ? Number(showtime_id) : null;

    const {
        data: reservation,
        isLoading,
        isError,
        refetch,
    } = useReservationDetail(Number.isFinite(bookingId) ? bookingId : null);

    useFocusEffect(
        useCallback(() => {
            refetch();
        }, [refetch])
    );

    useEffect(() => {
        const sub = AppState.addEventListener("change", (state) => {
            if (state === "active") {
                refetch();
            }
        });

        return () => sub.remove();
    }, [refetch]);

    const checkout = useCreateCheckoutSession();
    const cancel = useCancelReservation();

    const showtimeId = useMemo(() => {
        if (Number.isFinite(showtimeIdFromParams as number) && (showtimeIdFromParams as number) > 0) return showtimeIdFromParams as number;
        if (reservation?.showing_id) return reservation.showing_id;
        return null;
    }, [reservation?.showing_id, showtimeIdFromParams]);

    const createdLabel = useMemo(() => {
        if (!reservation?.created_at) return null;
        const d = new Date(reservation.created_at);
        return Number.isNaN(d.getTime()) ? reservation.created_at : d.toLocaleString();
    }, [reservation?.created_at]);

    const proceedToCheckout = async () => {
        if (!isAuthenticated) {
            Alert.alert("You need to be logged in to proceed.");
            router.push("/(auth)/login-view");
            return;
        }

        if (!Number.isFinite(bookingId)) {
            Alert.alert("Invalid reservation id.");
            return;
        }

        try {
            const session = await checkout.mutateAsync({ bookingId });

            const returnUrl = Linking.createURL("payment-return");

            const result = await WebBrowser.openAuthSessionAsync(session.url, returnUrl);

            if (result.type === "success" && result.url) {
                const parsed = Linking.parse(result.url);

                router.replace({
                    pathname: "/payment-return",
                    params: (parsed.queryParams ?? {}) as any,
                } as any);

                return;
            }

            refetch();
        } catch (err: any) {
            const message =
                (err?.response?.data?.detail as string) ||
                (err instanceof Error ? err.message : "Unknown error");
            Alert.alert("Checkout failed", message);
        }
    };

    const cancelReservation = async () => {
        if (!Number.isFinite(bookingId)) {
            Alert.alert("Invalid reservation id.");
            return;
        }

        try {
            await cancel.mutateAsync(bookingId);
            Alert.alert("Reservation cancelled");

            if (showtimeId) {
                router.replace(`/${showtimeId}/seat-selection-view`);
            } else {
                router.back();
            }
        } catch (err: any) {
            const message =
                (err?.response?.data?.detail as string) ||
                (err instanceof Error ? err.message : "Unknown error");
            Alert.alert("Cancel failed", message);
        }
    };

    if (!Number.isFinite(bookingId)) {
        return <ErrorScreen title="Invalid reservation" message="Reservation ID is missing or invalid." />;
    }

    if (isLoading) return <LoadingScreen message="Loading reservation..." />;

    if (isError || !reservation) {
        return <ErrorScreen message="Failed to load reservation." onRetry={refetch} />;
    }

    return (
        <SafeAreaView style={styles.safe}>
            <ScrollView contentContainerStyle={styles.content}>
                <View style={styles.header}>
                    <Text style={styles.title}>Reservation #{reservation.id}</Text>
                    <Text style={styles.sub}>Status: {reservation.status}</Text>
                    <Text style={styles.sub}>Total: {reservation.full_price}</Text>
                    {createdLabel ? <Text style={styles.sub}>Created: {createdLabel}</Text> : null}
                </View>

                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Tickets</Text>

                    {reservation.tickets?.length ? (
                        <View style={styles.ticketList}>
                            {reservation.tickets.map((t) => (
                                <View key={t.id} style={styles.ticketRow}>
                                    <Text style={styles.ticketText}>
                                        Row {t.seat_row}, Seat {t.seat_number}
                                    </Text>
                                    <Text style={styles.ticketPrice}>{t.price}</Text>
                                </View>
                            ))}
                        </View>
                    ) : (
                        <Text style={styles.empty}>No tickets.</Text>
                    )}
                </View>

                <View style={styles.actions}>
                    <Button
                        title="Proceed to payment"
                        onPress={proceedToCheckout}
                        isLoading={checkout.isPending}
                        disabled={cancel.isPending}
                        version="primary"
                    />

                    <Button
                        title="Cancel reservation"
                        onPress={cancelReservation}
                        isLoading={cancel.isPending}
                        disabled={checkout.isPending}
                        version="secondary"
                    />
                </View>
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    safe: {
        flex: 1,
        backgroundColor: theme.colors.background,
    },
    content: {
        padding: 16,
        gap: 18,
    },
    header: {
        gap: 6,
    },
    title: {
        color: theme.colors.textPrimary,
        fontSize: 20,
        fontWeight: "800",
    },
    sub: {
        color: theme.colors.textMuted,
    },
    section: {
        gap: 10,
        padding: 12,
        borderRadius: 10,
        borderWidth: 1,
        borderColor: theme.colors.textMuted,
    },
    sectionTitle: {
        color: theme.colors.textPrimary,
        fontWeight: "800",
        fontSize: 16,
    },
    ticketList: {
        gap: 10,
    },
    ticketRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
    },
    ticketText: {
        color: theme.colors.textPrimary,
    },
    ticketPrice: {
        color: theme.colors.textOnSecondary,
        fontWeight: "800",
    },
    empty: {
        color: theme.colors.textMuted,
    },
    actions: {
        gap: 10,
    },
});

export default ReservationDetailsView;

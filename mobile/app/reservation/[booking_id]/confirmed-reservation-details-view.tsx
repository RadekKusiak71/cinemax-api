import { useConfirmedReservationDetail } from "@/api/reservations";
import ErrorScreen from "@/components/ui/error-screen";
import LoadingScreen from "@/components/ui/loading-screen";
import { theme } from "@/constants/theme";
import { useLocalSearchParams } from "expo-router";
import React, { useMemo } from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function ConfirmedReservationDetailsView() {
    const { booking_id } = useLocalSearchParams<{ booking_id: string }>();
    const bookingId = Number(booking_id);

    const {
        data: reservation,
        isLoading,
        isError,
        refetch,
    } = useConfirmedReservationDetail(Number.isFinite(bookingId) ? bookingId : null);

    const createdLabel = useMemo(() => {
        if (!reservation?.created_at) return null;
        const d = new Date(reservation.created_at);
        return Number.isNaN(d.getTime()) ? reservation.created_at : d.toLocaleString();
    }, [reservation?.created_at]);

    const startLabel = useMemo(() => {
        if (!reservation?.showing_start_time) return null;
        const d = new Date(reservation.showing_start_time);
        return Number.isNaN(d.getTime()) ? reservation.showing_start_time : d.toLocaleString();
    }, [reservation?.showing_start_time]);

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
                    <Text style={styles.title}>{reservation.movie_title}</Text>
                    {startLabel ? <Text style={styles.sub}>{startLabel}</Text> : null}
                    <Text style={styles.sub}>Hall: {reservation.theater_hall}</Text>
                    <Text style={styles.sub}>Variant: {reservation.variant}</Text>
                </View>

                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Reservation</Text>
                    <Text style={styles.line}>ID: {reservation.id}</Text>
                    <Text style={styles.line}>Status: {reservation.status}</Text>
                    <Text style={styles.line}>Total: {reservation.full_price} €</Text>
                    {createdLabel ? <Text style={styles.line}>Created: {createdLabel}</Text> : null}
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
                                    <Text style={styles.ticketPrice}>{t.price} €</Text>
                                </View>
                            ))}
                        </View>
                    ) : (
                        <Text style={styles.empty}>No tickets.</Text>
                    )}
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    safe: {
        flex: 1,
        backgroundColor: theme.colors.background,
    },
    content: {
        padding: 16,
        gap: 16,
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
        gap: 8,
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
    line: {
        color: theme.colors.textPrimary,
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
});

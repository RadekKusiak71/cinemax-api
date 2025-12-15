import { useConfirmedReservations } from "@/api/reservations";
import ScreenHeader from "@/components/screen-header";
import ErrorScreen from "@/components/ui/error-screen";
import LoadingScreen from "@/components/ui/loading-screen";
import { theme } from "@/constants/theme";
import { useRouter } from "expo-router";
import React, { useMemo } from "react";
import { FlatList, Pressable, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function ReservationsHistoryView() {
    const router = useRouter();

    const {
        data,
        isLoading,
        isError,
        refetch,
    } = useConfirmedReservations({ limit: 50, offset: 0 });

    const items = useMemo(() => data?.results ?? [], [data?.results]);

    if (isLoading) return <LoadingScreen message="Loading reservations..." />;

    if (isError) {
        return <ErrorScreen message="Failed to load reservations." onRetry={refetch} />;
    }

    return (
        <SafeAreaView style={styles.safe}>
            <ScreenHeader title="My Bookings" />
            <FlatList
                contentContainerStyle={styles.content}
                data={items}
                keyExtractor={(item) => String(item.id)}
                ListEmptyComponent={
                    <View style={styles.empty}>
                        <Text style={styles.emptyTitle}>No reservations yet</Text>
                        <Text style={styles.emptyText}>Your confirmed reservations will appear here.</Text>
                    </View>
                }
                renderItem={({ item }) => {
                    const date = new Date(item.showing_start_time);
                    const when = Number.isNaN(date.getTime()) ? item.showing_start_time : date.toLocaleString();

                    return (
                        <Pressable
                            style={styles.card}
                            onPress={() =>
                                router.push({
                                    pathname: "/reservation/[booking_id]/confirmed-reservation-details-view",
                                    params: { booking_id: String(item.id) },
                                } as any)
                            }
                        >
                            <Text style={styles.title}>{item.movie_title}</Text>
                            <Text style={styles.sub}>{when}</Text>
                            <Text style={styles.sub}>Hall: {item.theater_hall}</Text>

                            <View style={styles.metaRow}>
                                <Text style={styles.meta}>{item.variant}</Text>
                                <Text style={styles.price}>{item.full_price} €</Text>
                            </View>
                        </Pressable>
                    );
                }}
            />
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    safe: {
        flex: 1,
        backgroundColor: theme.colors.background,
    },
    content: {
        padding: 12,
        gap: 12,
    },
    card: {
        padding: 12,
        borderRadius: 10,
        borderWidth: 1,
        borderColor: theme.colors.textMuted,
        backgroundColor: theme.colors.background,
        gap: 6,
    },
    title: {
        color: theme.colors.textPrimary,
        fontSize: 16,
        fontWeight: "800",
    },
    sub: {
        color: theme.colors.textMuted,
    },
    metaRow: {
        marginTop: 6,
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
    },
    meta: {
        color: theme.colors.textMuted,
    },
    price: {
        color: theme.colors.textPrimary,
        fontWeight: "800",
    },
    empty: {
        paddingVertical: 40,
        alignItems: "center",
        gap: 8,
    },
    emptyTitle: {
        color: theme.colors.textPrimary,
        fontSize: 18,
        fontWeight: "800",
    },
    emptyText: {
        color: theme.colors.textMuted,
        textAlign: "center",
    },
});

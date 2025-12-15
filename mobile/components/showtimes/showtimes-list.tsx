import { GroupedShowing } from "@/api/movies";
import TimeSlot from "@/components/showtimes/time-slot";
import { theme } from "@/constants/theme";
import React from "react";
import { StyleSheet, Text, View } from "react-native";
import LoadingScreen from "@/components/ui/loading-screen";

type ShowtimesListProps = {
    isLoading: boolean;
    showtimes?: GroupedShowing[];
    onTimePress: (showtimeId: number) => void;
};

export default function ShowtimesList({
    isLoading,
    showtimes,
    onTimePress,
}: ShowtimesListProps) {
    if (isLoading) return <LoadingScreen message="Loading showtimes..." />;

    const groups = showtimes ?? [];
    if (groups.length === 0) {
        return (
            <View style={styles.stateContainer}>
                <Text style={styles.stateText}>No showtimes available for this date.</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            {groups.map((group) => (
                <View key={group.variant_key} style={styles.group}>
                    <Text style={styles.variant}>{group.variant_key}</Text>

                    <View style={styles.grid}>
                        {group.showings.map((s) => (
                            <TimeSlot
                                key={s.id}
                                time={s.start_time}
                                onPress={() => onTimePress(s.id)}
                            />
                        ))}
                    </View>
                </View>
            ))}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        paddingHorizontal: 16,
        paddingVertical: 12,
        gap: 18,
        minHeight: 200,
    },
    group: {
        gap: 10,
    },
    variant: {
        fontSize: 13,
        fontWeight: "700",
        color: theme.colors.textMuted,
    },
    grid: {
        flexDirection: "row",
        flexWrap: "wrap",
        gap: 10,
    },
    stateContainer: {
        padding: 20,
        alignItems: "center",
    },
    stateText: {
        fontSize: 14,
        color: theme.colors.textMuted,
    },
});
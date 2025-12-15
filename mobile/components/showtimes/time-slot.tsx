import { theme } from "@/constants/theme";
import React, { useMemo } from "react";
import { StyleSheet, Text, TouchableOpacity } from "react-native";

interface TimeSlotProps {
    time: string;
    onPress: () => void;
}

const TimeSlot = ({ time, onPress }: TimeSlotProps) => {

    const { formattedTime, isPast } = useMemo(() => {
        const date = new Date(time);
        const now = new Date();

        const isPast = date < now;

        const formattedTime = date.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        });

        return { formattedTime, isPast };
    }, [time]);

    return (
        <TouchableOpacity
            disabled={isPast}
            onPress={onPress}
            activeOpacity={0.7}
            style={[
                styles.container,
                isPast && styles.containerPast,
            ]}
        >
            <Text
                style={[
                    styles.text,
                    isPast && styles.textPast
                ]}
            >
                {formattedTime}
            </Text>
        </TouchableOpacity>
    );
};

export default React.memo(TimeSlot);

const styles = StyleSheet.create({
    container: {
        borderWidth: 1,
        borderColor: theme.colors.primary,
        borderRadius: 4,
        paddingVertical: 8,
        paddingHorizontal: 16,
        minWidth: 70,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: theme.colors.background,
    },
    text: {
        fontSize: 13,
        fontWeight: '500',
        color: theme.colors.textPrimary,
    },
    containerPast: {
        backgroundColor: theme.colors.textMuted
    },
    textPast: {
        color: theme.colors.textOnPrimary,
    },
});
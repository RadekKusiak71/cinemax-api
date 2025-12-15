import { theme } from "@/constants/theme";
import { StyleSheet, Text, View } from "react-native";

const Pill = ({ label }: { label: string }) => {
    return (
        <View style={styles.pill}>
            <Text style={styles.pillText}>{label}</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    pill: {
        backgroundColor: theme.colors.background,
        paddingVertical: 8,
        paddingHorizontal: 15,
        borderRadius: 8,
        borderWidth: 1,
        borderColor: theme.colors.textMuted,
    },
    pillText: {
        color: theme.colors.textMuted,
        fontWeight: 'bold',
    },
});

export default Pill;
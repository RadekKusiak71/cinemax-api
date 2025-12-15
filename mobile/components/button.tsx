import { theme } from "@/constants/theme";
import React from "react";
import {
    ActivityIndicator,
    Pressable,
    StyleProp,
    StyleSheet,
    Text,
    TextStyle,
    ViewStyle
} from "react-native";

type ButtonProps = {
    title: string;
    onPress: () => void;
    disabled?: boolean;
    isLoading?: boolean;
    version?: "primary" | "secondary";
};

const Button: React.FC<ButtonProps> = ({ title, onPress, disabled, isLoading, version = "primary" }) => {

    const buttonStyles: StyleProp<ViewStyle> = [
        styles.baseButton,
        version === "primary" ? styles.primaryButton : styles.secondaryButton,
    ];

    const textStyles: StyleProp<TextStyle> = [
        styles.baseButtonText,
        version === "primary" ? styles.primaryButtonText : styles.secondaryButtonText,
    ];

    const spinnerColor = version === "primary" ? theme.colors.textPrimary : theme.colors.primary;

    return (
        <Pressable
            style={buttonStyles}
            onPress={onPress}
            disabled={disabled || isLoading}
        >
            {isLoading ? (
                <ActivityIndicator
                    testID="activity-indicator"
                    size="small"
                    color={spinnerColor}
                    style={{ marginRight: 8 }}
                />
            ) : (
                <Text style={textStyles}>{title}</Text>
            )}

        </Pressable>
    );
};

const styles = StyleSheet.create({
    baseButton: {
        paddingVertical: 12,
        paddingHorizontal: 24,
        borderRadius: 8,
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row',
        minHeight: 48,
    },
    baseButtonText: {
        fontSize: 16,
        fontWeight: '600',
    },
    primaryButton: {
        backgroundColor: theme.colors.primary,
    },
    primaryButtonText: {
        color: theme.colors.textOnPrimary,
    },
    secondaryButton: {
        borderWidth: 1.3,
        borderColor: theme.colors.primary,
    },
    secondaryButtonText: {
        color: theme.colors.primary,
    },
    disabledButton: {
        backgroundColor: theme.colors.textMuted,
        borderColor: theme.colors.textMuted,
    },
    disabledButtonText: {
        color: theme.colors.textMuted,
    }
});

export default Button;
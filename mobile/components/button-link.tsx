import { theme } from "@/constants/theme";
import { Href, useRouter } from "expo-router";
import React from "react";
import { StyleProp, StyleSheet, Text, TouchableOpacity, ViewStyle } from "react-native";

type ButtonLinkProps = {
    text: string;
    href: Href;
    variant?: 'primary' | 'secondary';
    style?: StyleProp<ViewStyle>;
}

const ButtonLink: React.FC<ButtonLinkProps> = ({ text, href, variant = 'primary', style }) => {
    const router = useRouter();

    const buttonStyle = variant === 'primary' ? styles.primaryButton : styles.secondaryButton;
    const textStyle = variant === 'primary' ? styles.primaryButtonText : styles.secondaryButtonText;

    return (
        <TouchableOpacity
            onPress={() => router.push(href)}
            style={[
                styles.baseButton,
                buttonStyle,
                style
            ]}
        >
            <Text style={textStyle}>{text}</Text>
        </TouchableOpacity>
    )
}

const styles = StyleSheet.create({
    baseButton: {
        width: '100%',
        paddingVertical: 18,
        borderRadius: 8,
        alignItems: 'center',
        justifyContent: 'center',
    },
    primaryButton: {
        backgroundColor: theme.colors.primary,
        borderWidth: 1.5,
        borderColor: theme.colors.primary,
    },
    secondaryButton: {
        backgroundColor: theme.colors.background,
        borderWidth: 1.5,
        borderColor: theme.colors.primary,
    },
    primaryButtonText: {
        color: theme.colors.textOnPrimary,
        fontWeight: '600',
    },
    secondaryButtonText: {
        color: theme.colors.primary,
        fontWeight: '600',
    }
})

export default ButtonLink;
import { theme } from "@/constants/theme";
import React from "react";
import { StyleSheet, Text, TextInput, TextInputProps, View } from "react-native";

interface FormInputProps extends TextInputProps {
    inputLabel: string;
    error?: string | string[];
}

const FormInput = ({ inputLabel, error, ...rest }: FormInputProps) => {
    const getInputStyle = () => {
        return [styles.input, error && styles.inputError];
    };

    return (
        <View>
            <Text style={styles.label}>{inputLabel}</Text>
            <TextInput testID="form-input" {...rest} style={getInputStyle()} />
            {error && <FormInputError error={error} />}
        </View>
    );
};

type FormInputErrorProps = {
    error: string | string[];
};

const FormInputError: React.FC<FormInputErrorProps> = ({ error }) => {
    return (
        <View>
            {Array.isArray(error) ? (
                error.map((errMsg, index) => (
                    <Text key={index} style={styles.errorText}>{errMsg}</Text>
                ))
            ) : (
                <Text style={styles.errorText}>{error}</Text>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    label: {
        marginBottom: 8,
        marginLeft: 5,
        fontSize: 16,
        color: theme.colors.textPrimary,
    },
    input: {
        paddingVertical: 15,
        paddingHorizontal: 10,
        backgroundColor: theme.colors.background,
        color: theme.colors.textPrimary,
        fontSize: 16,
        borderWidth: 1.2,
        borderColor: theme.colors.textPrimary,
        borderRadius: 5,
    },
    inputError: {
        borderColor: theme.colors.errorColor,
    },
    errorText: {
        color: theme.colors.errorColor,
        marginTop: 8,
        marginLeft: 2,
    },
});

export default FormInput;
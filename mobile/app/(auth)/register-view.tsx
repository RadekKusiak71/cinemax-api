import { registerUser } from "@/api/auth";
import Button from "@/components/button";
import FormInput from "@/components/form-input";
import RedirectLink from "@/components/redirect-link";
import TitleBlock from "@/components/title-block";
import { theme } from "@/constants/theme";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "expo-router";
import React from "react";
import { Alert, StyleSheet, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

type RegisterViewState = {
    form: {
        email: string;
        password: string;
        passwordConfirmation: string;
    },
    errors: {
        email?: string | string[];
        password?: string | string[];
        password_confirmation?: string | string[];
    },
}

const RegisterView = () => {
    const router = useRouter();
    const [state, setState] = React.useState<RegisterViewState>({
        form: {
            email: "",
            password: "",
            passwordConfirmation: "",
        },
        errors: {},
    });

    const onInputChange = (field: keyof RegisterViewState["form"], value: string) => {
        setState((prevState) => ({
            ...prevState,
            form: {
                ...prevState.form,
                [field]: value,
            },
        }));
    };

    const { mutate, isPending } = useMutation({
        mutationFn: registerUser,
        onSuccess: async () => {
            Alert.alert("Registration Successful", "You can now log in with your credentials.");
            router.replace("/login-view");
        },
        onError: (error: any) => {
            const data = error?.response?.data;

            const detail = data?.detail ?? data?.non_field_errors;
            if (detail) {
                Alert.alert(
                    "Registration failed",
                    Array.isArray(detail) ? detail.join("\n") : String(detail)
                );
                return;
            }

            setState((prev) => ({
                ...prev,
                errors: {
                    email: data?.email,
                    password: data?.password,
                    password_confirmation: data?.password_confirmation,
                },
            }));
        },
    });

    const onRegister = () => {
        setState((prev) => ({ ...prev, errors: {} }));
        mutate({
            email: state.form.email,
            password: state.form.password,
            passwordConfirmation: state.form.passwordConfirmation,
        });
    }

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.formContainer}>
                <TitleBlock title="Sign Up" subtitle="Enter your details to create an account." />

                <FormInput
                    inputLabel="Email"
                    placeholder="Enter your email"
                    error={state.errors.email}
                    value={state.form.email}
                    onChangeText={(value) => onInputChange('email', value)}
                    keyboardType="email-address"
                />

                <FormInput
                    inputLabel="Password"
                    placeholder="Enter your password"
                    error={state.errors.password}
                    value={state.form.password}
                    onChangeText={(value) => onInputChange('password', value)}
                    secureTextEntry
                />

                <FormInput
                    inputLabel="Confirm Password"
                    placeholder="Re-enter your password"
                    error={state.errors.password_confirmation}
                    value={state.form.passwordConfirmation}
                    onChangeText={(value) => onInputChange('passwordConfirmation', value)}
                    secureTextEntry
                />

                <Button title="Register" onPress={onRegister} isLoading={isPending} />
            </View>

            <RedirectLink text="Already have an account? " linkText="Sign In" href="/login-view" />
        </SafeAreaView>
    )
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 20,
        paddingHorizontal: 24,
        gap: 20,
        backgroundColor: theme.colors.background,
    },
    formContainer: {
        paddingTop: 10,
        width: '100%',
        gap: 17,
    }
});


export default RegisterView;
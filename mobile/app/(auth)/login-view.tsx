import { loginUser } from "@/api/auth";
import Button from "@/components/button";
import FormInput from "@/components/form-input";
import RedirectLink from "@/components/redirect-link";
import TitleBlock from "@/components/title-block";
import { theme } from "@/constants/theme";
import { useAuth } from "@/context/auth-context";
import { useMutation } from "@tanstack/react-query";
import { useLocalSearchParams, useRouter } from "expo-router";
import React from "react";
import { Alert, StyleSheet, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

type LoginViewState = {
	form: {
		email: string;
		password: string;
	};
	errors: {
		email?: string | string[];
		password?: string | string[];
	};
};

const LoginView = () => {
	const { login } = useAuth();
	const router = useRouter();
	const { redirect } = useLocalSearchParams<{ redirect?: string }>();

	const safeRedirect = React.useMemo(() => {
		if (!redirect || typeof redirect !== "string") return null;
		const decoded = (() => {
			try {
				return decodeURIComponent(redirect);
			} catch {
				return redirect;
			}
		})();

		if (!decoded.startsWith("/")) return null;
		if (decoded.startsWith("//")) return null;
		return decoded;
	}, [redirect]);

	const [state, setState] = React.useState<LoginViewState>({
		form: { email: "", password: "" },
		errors: {},
	});

	const onInputChange = (field: keyof LoginViewState["form"], value: string) => {
		setState((prev) => ({
			...prev,
			form: { ...prev.form, [field]: value },
			errors: { ...prev.errors, [field]: undefined },
		}));
	};

	const { mutate, isPending } = useMutation({
		mutationFn: loginUser,
		onSuccess: async (data) => {
			await login({ accessToken: data.access, refreshToken: data.refresh });

			if (safeRedirect) {
				router.replace(safeRedirect);
				return;
			}

			router.replace("/movies-list-view");
		},
		onError: (error: any) => {
			console.log("Login error:", error);
			const data = error?.response?.data;

			const detail = data?.detail ?? data?.non_field_errors;
			if (detail) {
				Alert.alert(
					"Login failed",
					Array.isArray(detail) ? detail.join("\n") : String(detail)
				);
				return;
			}

			setState((prev) => ({
				...prev,
				errors: {
					email: data?.email,
					password: data?.password,
				},
			}));
		},
	});

	const onLogin = () => {
		setState((prev) => ({ ...prev, errors: {} }));
		mutate({
			email: state.form.email,
			password: state.form.password,
		});
	};

	return (
		<SafeAreaView style={styles.container}>
			<View style={styles.formContainer}>
				<TitleBlock title="Sign In" subtitle="Welcome back! Glad to see you again." />

				<FormInput
					inputLabel="Email"
					placeholder="Enter your email"
					keyboardType="email-address"
					onChangeText={(text) => onInputChange("email", text)}
					error={state.errors.email}
					value={state.form.email}
				/>

				<FormInput
					inputLabel="Password"
					placeholder="Enter your password"
					secureTextEntry
					onChangeText={(text) => onInputChange("password", text)}
					error={state.errors.password}
					value={state.form.password}
				/>

				<Button title="Login" onPress={onLogin} isLoading={isPending} />
			</View>

			<RedirectLink text="Don't have an account? " linkText="Sign Up" href="/register-view" />
		</SafeAreaView>
	);
};

const styles = StyleSheet.create({
	container: {
		flex: 1,
		justifyContent: "space-between",
		alignItems: "center",
		padding: 20,
		paddingHorizontal: 24,
		gap: 20,
		backgroundColor: theme.colors.background,
	},
	formContainer: {
		paddingTop: 10,
		width: "100%",
		gap: 17,
	},
});

export default LoginView;

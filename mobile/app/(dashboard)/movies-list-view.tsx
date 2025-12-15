import { useMoviesInfinite } from "@/api/movies";
import MovieCard from "@/components/movies/movie-card";
import ScreenHeader from "@/components/screen-header";
import ErrorScreen from "@/components/ui/error-screen";
import LoadingScreen from "@/components/ui/loading-screen";
import { theme } from "@/constants/theme";
import { useRouter } from "expo-router";
import React from "react";
import { ActivityIndicator, FlatList, StyleSheet, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const MovieListView = () => {
    const router = useRouter();
    const {
        data,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
        isLoading,
        isRefetching,
        error,
        refetch,
    } = useMoviesInfinite();

    const movies = data?.pages.flatMap((p) => p.results) ?? [];

    const renderFooter = () => {
        if (!isFetchingNextPage) return null;
        return (
            <View style={styles.footer}>
                <ActivityIndicator />
            </View>
        );
    };

    if (isLoading) {
        return <LoadingScreen message="Loading Movies..." />;
    }

    if (error) {
        return <ErrorScreen message="Failed to load movies." onRetry={refetch} />;
    }

    return (
        <SafeAreaView style={styles.container}>
            <ScreenHeader title="Movies" />

            <FlatList
                data={movies}
                numColumns={2}
                keyExtractor={(item) => item.id.toString()}
                columnWrapperStyle={styles.columnWrapper}
                contentContainerStyle={styles.listContent}
                onRefresh={() => refetch()}
                refreshing={isRefetching && !isFetchingNextPage}
                onEndReached={() => {
                    if (hasNextPage && !isFetchingNextPage) fetchNextPage();
                }}
                onEndReachedThreshold={0.5}
                ListFooterComponent={renderFooter}
                renderItem={({ item }) => (
                    <View style={styles.cardContainer}>
                        <MovieCard movie={item} onPress={() => router.push(`/${item.id}/movie-details-view`)} />
                    </View>
                )}
            />
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: theme.colors.background,
    },
    listContent: {
        paddingHorizontal: 16,
        paddingTop: 16,
    },
    columnWrapper: {
        justifyContent: "space-between",
        marginBottom: 16,
    },
    cardContainer: {
        width: "48%",
    },
    footer: {
        paddingVertical: 20,
        alignItems: "center",
    },
});

export default MovieListView;

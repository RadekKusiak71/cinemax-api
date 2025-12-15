import { useMovieDetail, useMovieShowings } from "@/api/movies";
import MovieDetails from "@/components/movies/movie-details";
import DateStrip from "@/components/showtimes/date-strip";
import ShowtimesList from "@/components/showtimes/showtimes-list";
import { theme } from "@/constants/theme";
import { useLocalSearchParams, useRouter } from "expo-router";
import React, { useCallback, useState } from "react";
import { RefreshControl, ScrollView, StyleSheet } from "react-native";

const MovieDetailView = () => {
    const router = useRouter();
    const { movie_id } = useLocalSearchParams<{ movie_id: string }>();
    const [refreshing, setRefreshing] = useState(false);
    const [selectedDate, setSelectedDate] = useState<Date>(new Date());
    const formattedDate = selectedDate.toLocaleDateString('en-CA');

    const {
        data: movie,
        isLoading,
        isError,
        refetch,
    } = useMovieDetail(Number(movie_id));

    const {
        data: movieShowtimes,
        isLoading: isLoadingShowtimes,
        refetch: refetchShowtimes,
    } = useMovieShowings(Number(movie_id), formattedDate);


    const onRefresh = useCallback(async () => {
        setRefreshing(true);
        try {
            await Promise.all([refetch(), refetchShowtimes()]);
        } finally {
            setRefreshing(false);
        }
    }, [refetch, refetchShowtimes]);

    const handleTimePress = (showtimeId: number) => {
        router.push(`/${showtimeId}/seat-selection-view`);
    };

    return (
        <ScrollView
            style={styles.container}
            refreshControl={
                <RefreshControl
                    refreshing={refreshing}
                    onRefresh={onRefresh}
                    colors={[theme.colors.primary]}
                    tintColor={theme.colors.primary}
                />
            }
        >
            {movie && (
                <MovieDetails
                    movie={movie}
                    isLoading={isLoading}
                    isError={isError}
                />
            )}

            <DateStrip
                selectedDate={selectedDate}
                onSelectDate={setSelectedDate}
            />

            <ShowtimesList
                isLoading={isLoadingShowtimes}
                showtimes={movieShowtimes}
                onTimePress={handleTimePress}
            />
        </ScrollView>
    )
};

const styles = StyleSheet.create({
    container: {
        backgroundColor: theme.colors.background,
        flex: 1,
    },
});

export default MovieDetailView;
import apiClient from "@/api/client";
import { useInfiniteQuery, useQuery } from "@tanstack/react-query";

const PAGE_LIMIT = 20;

const MOVIES_URL = {
    listMovies: '/movies/',
    movieDetail: (id: number) => `/movies/${id}/`,
    movieShowings: (movieId: number) => `/movies/${movieId}/showings/`,
}

export type Movie = {
    id: number;
    title: string;
    poster_image: string;
    release_year: number;
}

export type Director = {
    id: number;
    first_name: string;
    last_name: string;
};

export type Genre = {
    id: number;
    name: string;
};

export type MovieDetail = {
    id: number;
    title: string;
    poster_image: string;
    release_year: number;
    duration: number;
    summary: string;
    original_language: string;
    director: Director;
    genres: Genre[];
};

export type Showing = {
    id: number;
    start_time: string;
};

export type GroupedShowing = {
    variant_key: string;
    showings: Showing[];
};

export type PaginatedMovies = {
    count: number;
    next: string | null;
    previous: string | null;
    results: Movie[];
}

type GetMoviesArgs = { pageParam?: number };

const getMovies = async ({ pageParam = 0 }: GetMoviesArgs): Promise<PaginatedMovies> => {
    const { data } = await apiClient.get(MOVIES_URL.listMovies, {
        params: { offset: pageParam, limit: PAGE_LIMIT },
    });
    return data;
};

const getMovieDetail = async (movieId: number): Promise<MovieDetail> => {
    const { data } = await apiClient.get(MOVIES_URL.movieDetail(movieId));
    return data;
};

type GetMovieShowingsArgs = {
    movieId: number;
    date?: string;
};

const getMovieShowings = async ({ movieId, date }: GetMovieShowingsArgs): Promise<GroupedShowing[]> => {
    const { data } = await apiClient.get(MOVIES_URL.movieShowings(movieId), {
        params: date ? { date } : undefined,
    });
    return data;
};

export function useMoviesInfinite() {
    return useInfiniteQuery({
        queryKey: ["movies"],
        queryFn: getMovies,
        initialPageParam: 0,
        getNextPageParam: (lastPage, allPages) => {
            if (!lastPage.next) return undefined;
            return allPages.length * PAGE_LIMIT;
        },
    });
}

export function useMovieDetail(movieId: number | null) {
    return useQuery({
        queryKey: ["movies", movieId],
        queryFn: () => getMovieDetail(movieId as number),
        enabled: typeof movieId === "number" && !Number.isNaN(movieId),
    });
}

export function useMovieShowings(movieId: number | null, date?: string) {
    return useQuery({
        queryKey: ["movies", movieId, "showings", date ?? null],
        queryFn: () => getMovieShowings({ movieId: movieId as number, date }),
        enabled: typeof movieId === "number" && !Number.isNaN(movieId),
    });
}
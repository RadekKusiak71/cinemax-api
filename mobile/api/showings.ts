import apiClient from "@/api/client";
import { useQuery } from "@tanstack/react-query";

const SHOWINGS_URL = {
    detail: (showingId: number) => `/showings/${showingId}/`,
    roomLayout: (showingId: number) => `/showings/${showingId}/room-layout/`,
};

export type RoomSeat = {
    id: number;
    row: number;
    number: number;
    is_reserved: boolean;
};

export type ShowingDetail = {
    id: number;
    start_time: string;
    end_time: string;
    theater_hall: string;
    movie: {
        id: number;
        title: string;
        summary: string;
        release_year: number;
        poster_image: string;
        duration: number;
        age_restriction: number;
        original_language: string;
        genres: Array<{
            id: number;
            name: string;
        }>;
        director: {
            id: number;
            first_name: string;
            last_name: string;
        };
    };
    variant: string;
};

const getShowingDetail = async (showingId: number): Promise<ShowingDetail> => {
    const { data } = await apiClient.get(SHOWINGS_URL.detail(showingId));
    return data;
};

export function useShowingDetail(showingId: number | null) {
    return useQuery({
        queryKey: ["showings", showingId, "detail"],
        queryFn: () => getShowingDetail(showingId as number),
        enabled: typeof showingId === "number" && Number.isFinite(showingId),
    });
}

const getRoomLayout = async (showingId: number): Promise<RoomSeat[]> => {
    const { data } = await apiClient.get(SHOWINGS_URL.roomLayout(showingId));
    return data;
};

export function useRoomLayout(showingId: number | null) {
    return useQuery({
        queryKey: ["showings", showingId, "room-layout"],
        queryFn: () => getRoomLayout(showingId as number),
        enabled: typeof showingId === "number" && Number.isFinite(showingId),
    });
}
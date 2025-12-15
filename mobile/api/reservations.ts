import apiClient from "@/api/client";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

const RESERVATIONS_URL = {
    list: () => `/reservations/`,
    detail: (bookingId: number | string) => `/reservations/${bookingId}/`,
    checkout: (bookingId: number) => `/reservations/${bookingId}/checkout/`,
};

export type ReservationStatus = "PENDING" | "EXPIRED" | "CONFIRMED" | "CANCELLED";

export type CreateReservationRequest = {
    showing_id: number;
    seat_ids: number[];
};

export type Reservation = {
    id: number;
    full_price: string;
    status: ReservationStatus;
    created_at: string;
    updated_at: string;
};

export type ConfirmedReservationListItem = {
    id: number;
    created_at: string;
    full_price: string;
    status: ReservationStatus;
    showing_id: number;
    showing_start_time: string;
    theater_hall: string;
    variant: string;
    movie_id: number;
    movie_title: string;
    movie_duration: number;
    movie_poster: string;
};

export type TicketInReservation = {
    id: number;
    price: string;
    seat_row: number;
    seat_number: number;
};

export type ConfirmedReservationDetail = ConfirmedReservationListItem & {
    tickets: TicketInReservation[];
};

export type ReservationDetail = ConfirmedReservationDetail;

export type Paginated<T> = {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
};

export type CheckoutSession = {
    session_id: string;
    url: string;
};

async function createReservation(body: CreateReservationRequest): Promise<Reservation> {
    const { data } = await apiClient.post(RESERVATIONS_URL.list(), body);
    return data;
}

async function listConfirmedReservations(params?: {
    limit?: number;
    offset?: number;
}): Promise<Paginated<ConfirmedReservationListItem>> {
    const { data } = await apiClient.get(RESERVATIONS_URL.list(), { params });
    return data;
}

async function getConfirmedReservation(bookingId: number | string): Promise<ConfirmedReservationDetail> {
    const { data } = await apiClient.get(RESERVATIONS_URL.detail(bookingId));
    return data;
}

async function getReservationDetail(bookingId: number | string): Promise<ReservationDetail> {
    const { data } = await apiClient.get(RESERVATIONS_URL.detail(bookingId));
    return data;
}

async function cancelPendingReservation(bookingId: number | string): Promise<void> {
    await apiClient.delete(RESERVATIONS_URL.detail(bookingId));
}

async function createStripeCheckoutSession(
    bookingId: number,
    body: Partial<CheckoutSession> = {}
): Promise<CheckoutSession> {
    const { data } = await apiClient.post(RESERVATIONS_URL.checkout(bookingId), body);
    return data;
}

export function useCreateReservation() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (body: CreateReservationRequest) => createReservation(body),
        onSuccess: (_reservation, variables) => {
            qc.invalidateQueries({ queryKey: ["showings", variables.showing_id, "room-layout"] });
            qc.invalidateQueries({ queryKey: ["reservations", "confirmed", "list"] });
        },
    });
}

export function useConfirmedReservations(params?: { limit?: number; offset?: number }) {
    return useQuery({
        queryKey: ["reservations", "confirmed", "list", params?.limit ?? null, params?.offset ?? null],
        queryFn: () => listConfirmedReservations(params),
    });
}

export function useConfirmedReservationDetail(bookingId: number | string | null) {
    return useQuery({
        queryKey: ["reservations", "confirmed", "detail", bookingId],
        queryFn: () => getConfirmedReservation(bookingId as number | string),
        enabled: bookingId !== null && bookingId !== undefined && bookingId !== "",
    });
}

export function useReservationDetail(bookingId: number | string | null) {
    return useQuery({
        queryKey: ["reservations", "detail", bookingId],
        queryFn: () => getReservationDetail(bookingId as number | string),
        enabled: bookingId !== null && bookingId !== undefined && bookingId !== "",
    });
}

export function useCancelReservation() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (bookingId: number | string) => cancelPendingReservation(bookingId),
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: ["reservations"] });
        },
    });
}

export function useCreateCheckoutSession() {
    return useMutation({
        mutationFn: ({ bookingId }: { bookingId: number }) => createStripeCheckoutSession(bookingId),
    });
}
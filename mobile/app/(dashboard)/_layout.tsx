import { theme } from "@/constants/theme";
import { useAuth } from "@/context/auth-context";
import FontAwesome from '@expo/vector-icons/FontAwesome';
import { Tabs } from "expo-router";
import React from "react";

const TabsLayout = () => {
    const { isAuthenticated } = useAuth();

    return (
        <Tabs initialRouteName="movies-list-view" screenOptions={{ headerShown: false, tabBarActiveTintColor: theme.colors.primary }}>
            <Tabs.Protected guard={isAuthenticated}>

                <Tabs.Screen
                    name='settings-view'
                    options={{
                        tabBarLabel: 'Settings',
                        tabBarIcon: ({ color }) => <FontAwesome name="cog" size={24} color={color} />,
                    }}
                />

                <Tabs.Screen
                    name='reservations-history-view'
                    options={{
                        tabBarLabel: 'Bookings',
                        tabBarIcon: ({ color }) => <FontAwesome name="ticket" size={24} color={color} />,
                    }}
                />
            </Tabs.Protected>

            <Tabs.Screen
                name='movies-list-view'
                options={{
                    tabBarLabel: 'Movies',
                    tabBarIcon: ({ color }) => <FontAwesome name="film" size={24} color={color} />,
                }}
            />
        </Tabs>
    )
};

export default TabsLayout;
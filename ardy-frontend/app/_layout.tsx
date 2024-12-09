import { Stack, Tabs, Link, Slot } from "expo-router";
import { setStatusBarStyle } from 'expo-status-bar';
import { useEffect } from "react";
import { SessionProvider } from "@/components/AuthContext";
import { Platform } from "react-native";

export default function RootLayout() {
  useEffect(() => {
    setTimeout(() => {
      setStatusBarStyle("dark");
    }, 0);
  }, []);


  return (
    <SessionProvider>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="(aux)/help" options={{ headerShown: false }} />
        <Stack.Screen name="(aux)/helpdesk-chat" options={{ headerShown: false }} />
        <Stack.Screen name="(aux)/privacy-policy" options={{ headerShown: false }} />
        <Stack.Screen name="(aux)/terms-of-service" options={{ headerShown: false }} />
        <Stack.Screen name="+not-found" />
      </Stack>
    </SessionProvider>
  );
}

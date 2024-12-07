import React, { useState } from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { Animated } from 'react-native';
import Header from '@/components/header';
import { useSession } from '../../components/AuthContext';

// Screen Components
import HomeScreen from './index';
import LoginScreen from './login';
import QuotationsScreen from './quotations';
import ProjectsScreen from './projects';
import ProfileScreen from './profile';
import OffersScreen from './offers';

// Create the Tab Navigator
const Tab = createBottomTabNavigator();

export default function TabLayout() {
  const { session, userType } = useSession();
  const [scrollY] = useState(new Animated.Value(0));

  // Render custom header with animated background
  const renderCustomHeader = (title: string, subtitle: string) => (
    <Animated.View
      style={{
        backgroundColor: scrollY.interpolate({
          inputRange: [0, 100],
          outputRange: ['#262b2e', '#2d363b'],
          extrapolate: 'clamp',
        }),
        zIndex: 10,
      }}
    >
      <Header title={title} subtitle={subtitle} />
    </Animated.View>
  );

  // A helper function to wrap screens and inject scroll logic
  const withScrollLogic = (Component: React.ComponentType) => (props: any) => (
    <Animated.ScrollView
      onScroll={Animated.event(
        [{ nativeEvent: { contentOffset: { y: scrollY } } }],
        { useNativeDriver: false }
      )}
      scrollEventThrottle={16}
    >
      <Component {...props} />
    </Animated.ScrollView>
  );

  // Function to determine which tabs to show
  const getTabs = () => {
    if (!session) {
      return (
        <>
          <Tab.Screen
            name="Home"
            component={withScrollLogic(HomeScreen)}
            options={{
              header: () => renderCustomHeader('Welcome Home', 'Explore your home dashboard!'),
              tabBarIcon: ({ focused, color }) => (
                <Ionicons name={focused ? 'home-sharp' : 'home-outline'} color={color} size={24} />
              ),
            }}
          />
          <Tab.Screen
            name="Offers"
            component={withScrollLogic(OffersScreen)}
            options={{
              header: () => renderCustomHeader('Special Offers', 'Check out the latest deals!'),
              tabBarIcon: ({ focused, color }) => (
                <Ionicons name={focused ? 'pricetags-sharp' : 'pricetags-outline'} color={color} size={24} />
              ),
            }}
          />
          <Tab.Screen
            name="Login"
            component={withScrollLogic(LoginScreen)}
            options={{
              header: () => renderCustomHeader('Login', 'Access your account now.'),
              tabBarIcon: ({ focused, color }) => (
                <Ionicons name={focused ? 'log-in-sharp' : 'log-in-outline'} color={color} size={24} />
              ),
            }}
          />
        </>
      );
    }

    if (userType === 'Customer') {
      return (
        <>
          <Tab.Screen
            name="Home"
            component={withScrollLogic(HomeScreen)}
            options={{
              header: () => renderCustomHeader('Welcome', 'Explore your home dashboard!'),
              tabBarIcon: ({ focused, color }) => (
                <Ionicons name={focused ? 'home-sharp' : 'home-outline'} color={color} size={24} />
              ),
            }}
          />
          <Tab.Screen
            name="Offers"
            component={withScrollLogic(OffersScreen)}
            options={{
              header: () => renderCustomHeader('Special Offers', 'Check out the latest deals!'),
              tabBarIcon: ({ focused, color }) => (
                <Ionicons name={focused ? 'pricetags-sharp' : 'pricetags-outline'} color={color} size={24} />
              ),
            }}
          />
          <Tab.Screen
            name="Quotations"
            component={withScrollLogic(QuotationsScreen)}
            options={{
              header: () => renderCustomHeader('Quotations', 'View and manage your quotes.'),
              tabBarIcon: ({ focused, color }) => (
                <Ionicons name={focused ? 'document-sharp' : 'document-outline'} color={color} size={24} />
              ),
            }}
          />
          <Tab.Screen
            name="Projects"
            component={withScrollLogic(ProjectsScreen)}
            options={{
              header: () => renderCustomHeader('Your Projects', 'Manage your ongoing projects.'),
              tabBarIcon: ({ focused, color }) => (
                <Ionicons name={focused ? 'hammer-sharp' : 'hammer-outline'} color={color} size={24} />
              ),
            }}
          />
          <Tab.Screen
            name="Profile"
            component={withScrollLogic(ProfileScreen)}
            options={{
              header: () => renderCustomHeader('Your Profile', 'Update your profile information.'),
              tabBarIcon: ({ focused, color }) => (
                <Ionicons name={focused ? 'person-circle-sharp' : 'person-circle-outline'} color={color} size={24} />
              ),
            }}
          />
        </>
      );
    }

    return null;
  };

  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#7bd3ce',
        tabBarStyle: {
          backgroundColor: '#2d363b',
        },
        headerShown: true,
      }}
    >
      {getTabs()}
    </Tab.Navigator>
  );
}

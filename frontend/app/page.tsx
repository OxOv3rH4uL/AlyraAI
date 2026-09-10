"use client";

import { useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Spinner } from "@/components/ui/spinner";

interface Room {
  name: string;
  room_type: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

interface FloorBoundary {
  width: number;
  height: number;
}

interface FloorPlan {
  floor: number;
  boundary: FloorBoundary;
  rooms: Room[];
}

interface PlanResponse {
  total_area: number;
  status: string;
  floors: number;
  floor_plan: FloorPlan[];
  svg: string;
}

export default function Home() {
  const [description, setDescription] = useState("");
  const [plan, setPlan] = useState<PlanResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generatePlan = async () => {
    if (!description.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setPlan(null);

    try {
      const response = await axios.post(
        "http://localhost:8000/api/v1/plans/generate",
        {
          description: description,
        }
      );

      const data: PlanResponse = response.data;
      setPlan(data);
    } catch (error) {
      console.error(error);

      setError(
        "Something went wrong while generating your house plan. Please try again."
      );
    } finally {
      setLoading(false);
    }

  };

  return (
    <main className="min-h-screen bg-background px-6 py-12">
      <div className="mx-auto flex max-w-5xl flex-col items-center">
        {/* Header */}
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-bold tracking-tight">
            Alyra AI
          </h1>

          <p className="mt-3 text-muted-foreground">
            Describe your dream home and let AI design the floor plan.
          </p>
        </div>

        {/* Input */}
        <Card className="w-full max-w-2xl">
          <CardHeader>
            <CardTitle>Describe your home</CardTitle>

            <CardDescription>
              Tell Alyra what kind of house you want. Include rooms(as of now XD)
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4">
            <Textarea
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Example: I need a modern house with 2 bedrooms, a kitchen, a spacious living room and 2 bathrooms."
              className="min-h-[160px] resize-none"
              disabled={loading}
            />

            <Button
              onClick={generatePlan}
              disabled={loading || !description.trim()}
              className="w-full"
            >
              {loading ? (
                <>
                  <Spinner />
                  Generating house plan...
                </>
              ) : (
                "Generate House Plan"
              )}
            </Button>

            {/* Error */}
            {error && (
              <p className="text-sm text-destructive">
                {error}
              </p>
            )}
          </CardContent>
        </Card>

        {/* Loading */}
        {loading && (
          <div className="mt-10 flex flex-col items-center gap-3 text-center">
            <Spinner className="size-8" />

            <div>
              <p className="font-medium">
                Designing your house...
              </p>

              <p className="text-sm text-muted-foreground">
                AI is generating and validating your floor plan.
              </p>
            </div>
          </div>
        )}

        {/* Result */}
        {plan && !loading && (
          <Card className="mt-10 w-full">
            <CardHeader>
              <CardTitle>Your House Plan</CardTitle>

              <CardDescription>
                Generated successfully
              </CardDescription>
            </CardHeader>

            <CardContent>
              {/* Plan information */}
              <div className="mb-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
                <div className="rounded-lg border p-4">
                  <p className="text-sm text-muted-foreground">
                    Total Area
                  </p>

                  <p className="mt-1 text-xl font-semibold">
                    {plan.total_area.toFixed(2)} m²
                  </p>
                </div>

                <div className="rounded-lg border p-4">
                  <p className="text-sm text-muted-foreground">
                    Floors
                  </p>

                  <p className="mt-1 text-xl font-semibold">
                    {plan.floors}
                  </p>
                </div>

                <div className="rounded-lg border p-4">
                  <p className="text-sm text-muted-foreground">
                    Rooms
                  </p>

                  <p className="mt-1 text-xl font-semibold">
                    {plan.floor_plan.reduce(
                      (total, floor) => total + floor.rooms.length,
                      0
                    )}
                  </p>
                </div>
              </div>

              {/* SVG */}
              <div className="overflow-auto rounded-xl border bg-white p-4">
                <div
                  className="flex justify-center"
                  dangerouslySetInnerHTML={{
                    __html: plan.svg,
                  }}
                />
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  );
}
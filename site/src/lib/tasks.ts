import tasksData from "../data/tasks.json";
import { graphNodes } from "./graph";
import type { Task } from "./types";

const tasks = tasksData as Task[];

/* Build-time validation against known graph skills (no fs dependency) */

const knownSkillIds = new Set(graphNodes.map((n) => n.id));
const knownPluginSlugs = new Set(graphNodes.map((n) => n.plugin));

for (const task of tasks) {
  if (!task.id || !task.title) {
    throw new Error(`Task missing id or title: ${JSON.stringify(task)}`);
  }
  for (const id of task.skillIds) {
    if (!knownSkillIds.has(id)) {
      throw new Error(`Task "${task.id}" references unknown skill "${id}"`);
    }
  }
  for (const slug of task.relatedPluginSlugs) {
    if (!knownPluginSlugs.has(slug)) {
      throw new Error(`Task "${task.id}" references unknown plugin "${slug}"`);
    }
  }
}

/* Public API */

export function getAllTasks(): Task[] {
  return tasks;
}

export function getTask(id: string): Task | undefined {
  return tasks.find((t) => t.id === id);
}

export function getTasksByPlugin(slug: string): Task[] {
  return tasks.filter((t) => t.relatedPluginSlugs.includes(slug));
}

export function getTasksContainingSkill(skillId: string): Task[] {
  return tasks.filter((t) => t.skillIds.includes(skillId));
}

export const relationTypes = [
  "enhancement",
  "prerequisite",
  "calls",
  "produces_for",
  "alternative",
] as const;

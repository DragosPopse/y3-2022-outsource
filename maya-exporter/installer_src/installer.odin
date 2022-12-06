package main

import "core:fmt"
import "core:os"
import win32 "core:sys/windows"
import intr "core:intrinsics"
import "core:strings"
import "core:path/filepath"

L :: intr.constant_utf16_cstring

// Thanks hikari from odin discord, a true win32 wizard ;)
fully_qualify_path :: proc(p: string, allocator := context.allocator) -> string {
    if filepath.volume_name(p) != "" do return p

    cur_dir := os.get_current_directory(context.temp_allocator)
    return filepath.join({cur_dir, p}, allocator)
}

copy_file :: proc(from, to: string) -> i32 {
    from := fully_qualify_path(from, context.temp_allocator)
    to := fully_qualify_path(to, context.temp_allocator)

    file_op: win32.SHFILEOPSTRUCTW = {
        nil,
        win32.FO_COPY,
        win32.utf8_to_wstring(fmt.tprintf("{}\x00", from)), // the string must be double-null terminated
        win32.utf8_to_wstring(fmt.tprintf("{}\x00", to)),
        win32.FOF_NOCONFIRMATION | win32.FOF_NOERRORUI | win32.FOF_SILENT,
        false,
        nil,
        nil,
    }
    return win32.SHFileOperationW(&file_op)
}

copy_tool :: proc(scripts_path: string) {
    toolDirPath := strings.concatenate({scripts_path, `\PipelineTool`})
    os.make_directory(toolDirPath)
    
    if dirfd, err := os.open("PipelineTool"); err == os.ERROR_NONE {
        defer os.close(dirfd)
        if files, err := os.read_dir(dirfd, 0); err == os.ERROR_NONE {
            for file in files {
                destFilePath := strings.concatenate({toolDirPath, `\`, file.name})
                fmt.printf("Copying %s to %s\n", file.name, destFilePath)
                copy_file(file.fullpath, destFilePath)
            }
        } else {
            fmt.printf("Error %d: Failed to read PipelineTool directory", err)
        } 
    } else {
        fmt.printf("Error %d: Failed to open PipelineTool directory", err)
    }
}

write_user_setup :: proc(scripts_path: string) {
    userSetupPath := strings.concatenate({scripts_path, `\userSetup.py`})
    importStmt := "import PipelineTool"
    prevSetup: []byte
    prevSetupStr: string
    containsImport := false
    if out, ok := os.read_entire_file_from_filename(userSetupPath); ok {
        prevSetup = out 
        prevSetupStr := strings.string_from_ptr(&prevSetup[0], len(prevSetup))

        lineIter := prevSetupStr 
        for line in strings.split_lines_iterator(&lineIter) {
            if strings.index(line, importStmt) != -1 {
                containsImport = true
                fmt.printf("Found PipelineTool import statement in userSetup.py. Skipping setup.\n")
                return
            }
        }
    } else {
        fmt.printf("Couldn't find previous userSetup.py, creating a new file.\n")
    }

    if setupFile, err := os.open(userSetupPath, os.O_CREATE | os.O_TRUNC | os.O_WRONLY); err == os.ERROR_NONE {
        defer os.close(setupFile)
        sb := strings.builder_make()
        using strings 
        write_string(&sb, importStmt)
        write_string(&sb, "\n")
        write_string(&sb, prevSetupStr)
        fmt.printf("Writing userSetup.py\n")
        fmt.fprintf(setupFile, "%s", strings.to_string(sb))
    } else {
        fmt.printf("Error %d: couldn't create setup file %s\n", err, userSetupPath)
    }
}


main :: proc() {
    if ODIN_OS != .Windows {
        fmt.printf("Error: This installer is only available for the windows version of maya.\n")
        return
    }
    wpath: [255]win32.WCHAR
    
    if !win32.SUCCEEDED(win32.SHGetFolderPathW(nil, win32.CSIDL_PROFILE, nil, 0, &wpath[0])) {
        fmt.printf("Error: Failed to get the user folder\n")
        return 
    } 

    userPath, _ := win32.wstring_to_utf8(&wpath[0], -1)
    fmt.printf("Found user folder %s\n", userPath)
    mayaScripts := strings.concatenate({userPath, `\Documents\maya\2023\scripts`})
    if !os.is_dir(mayaScripts) {
        fmt.printf("Error: Couldn't find maya scripts folder %s\n", mayaScripts)
        return
    } 
    fmt.printf("Found maya scripts folder %s\n", mayaScripts)
    copy_tool(mayaScripts)
    write_user_setup(mayaScripts)
    fmt.printf("Installation complete. Enjoy your new tool!\n")
}